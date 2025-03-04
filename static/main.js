// Habit Creation
document.getElementById('habitForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch('/add_task', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: formData.get('name'),
                score_amount: formData.get('score'),
                group_id: formData.get('groupId')
            })
        });

        if (response.ok) window.location.reload();
    } catch (error) {
        alert('Error creating habit');
    }
});

// Complete Habit
document.querySelectorAll('.complete-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
        const taskId = e.target.dataset.taskId;
        
        try {
            const response = await fetch('/complete_task', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ task_id: taskId })
            });

            if (response.ok) window.location.reload();
        } catch (error) {
            alert('Error completing habit');
        }
    });
});