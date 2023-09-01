(function() {
    console.log('Mega-Web is started up and ready to use!');
  })();

  function handleClick(task_type) {
    const form = document.getElementById(`Form${task_type}`);
    const data = new FormData(form);
    const values = Object.fromEntries(data.entries());

    fetch('/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Mega-Task': task_type
      },
      body: JSON.stringify(values),  // JSON.stringify({ task: task_type }),
    })
    .then(response => response.json())
    .then(data => getStatus(data.task_id));
  }

  function getStatus(taskID) {
    fetch(`/tasks/${taskID}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    })
    .then(response => response.json())
    .then(res => {
      const html = `
        <tr>
          <td>${taskID}</td>
          <td>${res.task_status}</td>
          <td>${res.task_result}</td>
        </tr>`;

      const existsRow = document.getElementById(taskID);
      if (existsRow === null) {
        const newRow = document.getElementById('tasks').insertRow(0);
        newRow.setAttribute("id", taskID);
        newRow.innerHTML = html;
      } else {
        existsRow.innerHTML = html;
      }

      const taskStatus = res.task_status;
      if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
      setTimeout(function() {
        getStatus(res.task_id);
      }, 1000);
    })
    .catch(err => console.log(err));
}