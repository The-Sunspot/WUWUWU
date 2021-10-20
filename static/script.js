function myFunction(x) {
    // 声明变量
    var input, filter, table, tr, td, i;
    input = document.getElementById("myInput"+x);
    document.getElementById("myInput"+(1-x)).value="";
    filter = input.value.toUpperCase();
    table = document.getElementById("table");
    tr = table.getElementsByTagName("tr");
  
    // 循环表格每一行，查找匹配项
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[x];
      if (td) {
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      } 
    }
  }
  function sum1(n) {
    var total = 0.0,high=0.0;
    for (i = 1; i <= n; i++) {
      txt = document.getElementById(eval("'"  + i+ '1' + "'")).value;
      txt2 = document.getElementById(eval("'"  + i+ '2' + "'")).value;
      if (txt != ""&& txt2!="") {
        total += parseFloat(txt)*parseFloat(txt2)/100.0;
        high=Math.max(high,txt2);
      }
    }

    document.getElementById('highscore').value=parseFloat(document.getElementById("12").value).toFixed(2) ;
    document.getElementById('average').value=total.toFixed(2);
  }