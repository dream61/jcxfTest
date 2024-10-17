from celery import shared_task
from apscheduler.schedulers.background import BackgroundScheduler  
from testscenario.models import TestScenario  
from test_reports.models import TestReport  
from testresult.models import TestResult  
from test_case_management.models import TestCase
from scheduled_tasks.models import ScheduledTask
from django.utils.timezone import now  
import unittest  
from .lib.HTMLTestRunner import HTMLTestRunner  
import os,logging
import requests,json
from django.core.mail import send_mail
from django.conf import settings
from pytz import timezone
from apscheduler.triggers.cron import CronTrigger
  
@shared_task  
def run_scenario_testcases(test_result_id): 
    logging.info(f"开始执行测试用例，TestResult ID: {test_result_id}")
 
    test_result = TestResult.objects.get(id=test_result_id)  
    scenario = test_result.scenario  
  
    class TestSuite(unittest.TestCase):  
        pass  
  
    def create_test_method(test_case):  
        def test_method(self):
            try:
                url = test_case.host_url.environment_value+test_case.url
                method = test_case.request_method
                headers = test_case.headers
                data = test_case.request_data
                bodycontent = test_case.body
                expected_response = test_case.expected_response
            except AttributeError as e:
                self.fail(f"测试用例 '{test_case.name}' 缺少必要的属性: {str(e)}")
                return
              
            try:  
                if method == 'GET':  
                    response = requests.get(url,headers=headers, data=data)  
                elif method == 'POST':  
                    response = requests.post(url, headers=headers, json=json.loads(bodycontent))  
                elif method == 'PUT':  
                    response = requests.put(url, headers=headers, json=json.loads(bodycontent))  
                elif method == 'DELETE':  
                    response = requests.delete(url, headers=headers,data=data)  
                elif method == 'PATCH':
                    response = requests.patch(url, json=json.loads(bodycontent))
                elif method == 'HEAD':
                    response = requests.head(url,headers=headers, data=data)  
                elif method == 'OPTIONS':
                    response = requests.options(url,headers=headers, data=data)     
                else:  
                    self.fail(f"不支持的请求方法: {method}")  
                  
                self.assertEqual(response.json(), expected_response, f"测试用例 '{test_case.name}' 失败，返回的状态码为 {response.status_code}")  
            except requests.RequestException as e: 
                logging.info(f"url为: {url}") 
                self.fail(f"测试用例 '{test_case.name}' 失败，HTTP 请求错误: {str(e)}")  
          
        return test_method  
  
    for test_case in scenario.test_cases.all():  
        test_method_name = f'test_{test_case.name}'  
        test_method = create_test_method(test_case)  
        setattr(TestSuite, test_method_name, test_method)  
  
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSuite)  
  
    report_dir = 'reports/'  
    if not os.path.exists(report_dir):  
        os.makedirs(report_dir)  
    report_path = os.path.join(report_dir, f'{scenario.name}_{now().strftime("%Y%m%d%H%M%S")}.html')
    logging.info(f"测试报告路径: {report_path}")
  
    with open(report_path, 'wb') as report_file:
        runner = HTMLTestRunner(stream=report_file, verbosity=2, title=f'{scenario.name} 测试报告')
        result = runner.run(suite)  # 保存测试结果

    if len(result.failures) == 0 and len(result.errors) == 0:  # 检查失败的测试用例数量
       test_result.status = 'success'
       test_result.report_file=report_path
    else:
       test_result.status = 'fail'
       test_result.report_file=report_path
  
    test_result.save()
    test_result.refresh_from_db()
    logging.info(f"测试结果已保存: 状态 - {test_result.status}")  
  
    TestReport.objects.create(test_result=test_result, report_file=report_path)
    logging.info(f"测试报告已生成并保存到数据库")




def run_scheduled_task(task_id):
    task = ScheduledTask.objects.get(id=task_id)
    logging.info(f"开始执行任务: {task.name}")
    task.status = 'running'
    task.save()

    # 创建 TestResult 对象
    test_result = TestResult.objects.create(
        scenario=task.testscenario,
        status='running',
        executed_by=task.created_by
    )
    
    # 执行测试用例
    result = run_scenario_testcases.apply_async(args=[test_result.id])
    result.get()
    test_result.refresh_from_db()
    recipient_email = task.email

    # 根据测试结果发送邮件
    if test_result.status == 'success' or test_result.status == 'fail':
        send_report_email(test_result.report_file, recipient_email)
    else:
        logging.warning(f"任务 {task.name} 测试结果为 {test_result.status}，未发送邮件。")
    
    task.status = 'completed'
    task.save()
    logging.info(f"任务 {task.name} 已完成")
        
        


def send_report_email(report_file, recipient_email):
    logging.info(f"准备发送邮件至: {recipient_email}，报告文件: {report_file}")
    try:
        with open(report_file, 'r') as f:
            report_content = f.read()

        send_mail(
            subject='测试报告',
            message='请查收附件中的测试报告。',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
            html_message=report_content
        )
        logging.info(f"邮件已成功发送至: {recipient_email}")
    except Exception as e:
        logging.error(f"发送邮件时出错: {e}")


def schedule_tasks():
    statuses = ['pendding', 'failed', 'completed'] 
    tasks = ScheduledTask.objects.filter(status__in=statuses)
    scheduler = BackgroundScheduler(timezone=timezone('Asia/Shanghai'))
    
    for task in tasks:
        cron_expression = task.cron_expression
        cron_parts = cron_expression.split()  # 假设 cron 表达式为标准的 5 部分或 6 部分
        
        # 使用 cron 表达式动态创建任务
        scheduler.add_job(
            run_scheduled_task, 
            trigger=CronTrigger(minute=cron_parts[0], hour=cron_parts[1], 
                                day=cron_parts[2], month=cron_parts[3], 
                                day_of_week=cron_parts[4]),
            args=[task.id],
            id=str(task.id)
        )
    
    scheduler.start()
    logging.info("APScheduler 调度器已启动")

schedule_tasks()