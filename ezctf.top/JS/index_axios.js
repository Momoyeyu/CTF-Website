window.addEventListener('DOMContentLoaded', function() {  
    axios.get('http://localhost:80/api/task/list?action=list_all&type=0&is_login=1&user_id=0') // 修改为你的本地服务器地址  
      .then(function(response) {  
        const data=response.data;          
        const item=data.retlist[0];
        const questionname=document.getElementById('question-name');
        const questionsource=document.getElementById('question-source');
        const questionscore=document.getElementById('question-score');
        const questionamount=document.getElementById('question-amount');
        questionname.textContent=`${item.task_name}`;
        questionsource.textContent=`来源：${item.src}`;
        questionscore.textContent=`分数：${item.points}`;
        questionamount.textContent=`解出人数：${item.solve_count}`;
      })  
      .catch(function() {  
      });
});
document.addEventListener('DOMContentLoaded', function() {  
    document.getElementById('sendRequest0').addEventListener('click', function() {  
      axios.get('http://localhost:80/api/task/list?action=list_all&type=0&is_login=1&user_id=0') // 修改为你的本地服务器地址  
        .then(function(response) {  
          const data=response.data;          
          const item=data.retlist[0];
          const questionname=document.getElementById('question-name');
          const questionsource=document.getElementById('question-source');
          const questionscore=document.getElementById('question-score');
          const questionamount=document.getElementById('question-amount');
          questionname.textContent=`${item.task_name}`;
          questionsource.textContent=`来源：${item.src}`;
          questionscore.textContent=`分数：${item.points}`;
          questionamount.textContent=`解出人数：${item.solve_count}`;
        })  
        .catch(function() {  
        });  
    });  
  });
  document.addEventListener('DOMContentLoaded', function() {  
    document.getElementById('sendRequest1').addEventListener('click', function() {  
      axios.get('http://localhost:80/api/task/list?action=list_all&type=1&is_login=1&user_id=0') // 修改为你的本地服务器地址  
        .then(function(response) {  
          const data=response.data;          
          const item=data.retlist[0];
          const questionname=document.getElementById('question-name1');
          const questionsource=document.getElementById('question-source1');
          const questionscore=document.getElementById('question-score1');
          const questionamount=document.getElementById('question-amount1');
          questionname.textContent=`${item.task_name}`;
          questionsource.textContent=`来源：${item.src}`;
          questionscore.textContent=`分数：${item.points}`;
          questionamount.textContent=`解出人数：${item.solve_count}`;
        })  
        .catch(function() {  
        });  
    });  
  });
  document.addEventListener('DOMContentLoaded', function() {  
    document.getElementById('sendRequest2').addEventListener('click', function() {  
      axios.get('http://localhost:80/api/task/list?action=list_all&type=2&is_login=1&user_id=0') // 修改为你的本地服务器地址  
        .then(function(response) {  
          const data=response.data;
          console.log(data);          
          const item=data.retlist[0];
          const questionname=document.getElementById('question-name2');
          const questionsource=document.getElementById('question-source2');
          const questionscore=document.getElementById('question-score2');
          const questionamount=document.getElementById('question-amount2');
          questionname.textContent=`${item.task_name}`;
          questionsource.textContent=`来源：${item.src}`;
          questionscore.textContent=`分数：${item.points}`;
          questionamount.textContent=`解出人数：${item.solve_count}`;
        })  
        .catch(function() {  
        });  
    });  
  });
  document.addEventListener('DOMContentLoaded', function() {  
    document.getElementById('sendRequest3').addEventListener('click', function() {  
      axios.get('http://localhost:80/api/task/list?action=list_all&type=3&is_login=1&user_id=0') // 修改为你的本地服务器地址  
        .then(function(response) {  
          const data=response.data;          
          const item=data.retlist[0];
          const questionname=document.getElementById('question-name3');
          const questionsource=document.getElementById('question-source3');
          const questionscore=document.getElementById('question-score3');
          const questionamount=document.getElementById('question-amount3');
          questionname.textContent=`${item.task_name}`;
          questionsource.textContent=`来源：${item.src}`;
          questionscore.textContent=`分数：${item.points}`;
          questionamount.textContent=`解出人数：${item.solve_count}`;
        })  
        .catch(function() {  
        });  
    });  
  });
  document.addEventListener('DOMContentLoaded', function() {  
    document.getElementById('sendRequest4').addEventListener('click', function() {  
      axios.get('http://localhost:80/api/task/list?action=list_all&type=4&is_login=1&user_id=0') // 修改为你的本地服务器地址  
        .then(function(response) {  
          const data=response.data;          
          const item=data.retlist[0];
          const questionname=document.getElementById('question-name4');
          const questionsource=document.getElementById('question-source4');
          const questionscore=document.getElementById('question-score4');
          const questionamount=document.getElementById('question-amount4');
          questionname.textContent=`${item.task_name}`;
          questionsource.textContent=`来源：${item.src}`;
          questionscore.textContent=`分数：${item.points}`;
          questionamount.textContent=`解出人数：${item.solve_count}`;
        })  
        .catch(function() {  
        });  
    });  
  });
  // document.addEventListener('DOMContentLoaded', function() {  
  //   document.getElementById('trigger').addEventListener('click', function() {  
  //     axios.post('http://localhost:80/api/task/list?action=query_one&task_id=1')
  //       .then(function(response) {  
  //         const data=response.data;          
  //         const item=data.retlist[0];
  //         const questionname=document.getElementById('question-name4');
  //         const questionsource=document.getElementById('question-source4');
  //         const questionscore=document.getElementById('question-score4');
  //         const questionamount=document.getElementById('question-amount4');
  //         questionname.textContent=`${item.task_name}`;
  //         questionsource.textContent=`来源：${item.src}`;
  //         questionscore.textContent=`分数：${item.points}`;
  //         questionamount.textContent=`解出人数：${item.solve_count}`;
  //       })  
  //       .catch(function() {  
  //       });  
  //   });  
  // });