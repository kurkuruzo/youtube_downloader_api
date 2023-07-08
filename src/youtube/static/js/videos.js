function checkTaskStatus(task_id) {
    console.log(task_id)
    fetch("/api/videos/status?task_id=" + task_id)
        .then((res) => res.json())
        .then((data) => {
            console.log(data)
            let status_field = document.getElementById("status")
            status_field.style.fontWeight = "bold"
            if (data.status == "SUCCESS") {
                status_field.innerText = "Загрузка завершена"
                status_field.style.color = "green"
            } else if (data.status == "SUCCESS") {
                status_field.innerText = "Выполняется загрузка"
                status_field.style.color = "red"
            } else {
                setTimeout(checkTaskStatus, 1000, task_id)
            }
        })
}

checkTaskStatus(task_id)
