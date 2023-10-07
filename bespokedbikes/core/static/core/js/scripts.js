function setToday() {
    var today = new Date();
    var year = today.getFullYear();
    var month = (today.getMonth() + 1).toString().padStart(2, '0'); // Month is 0-indexed, so add 1
    var day = today.getDate().toString().padStart(2, '0');
    var formattedDate = year + '-' + month + '-' + day;
    document.getElementById('sales_date').value = formattedDate
}
document.addEventListener("DOMContentLoaded", function() {
    setToday();
});