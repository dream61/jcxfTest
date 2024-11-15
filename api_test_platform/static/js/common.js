function changePerPage(value) {
    // 获取当前页面的URL
    var currentUrl = window.location.href;
    // 去除原有的page和per_page参数（如果有的话）
    currentUrl = currentUrl.split('?')[0];
    // 添加新的per_page参数和选择的值，并设置page参数为1，表示定位到第一页
    currentUrl += '?page=1&per_page=' + value;
    // 跳转到新的URL
    window.location.href = currentUrl;
}