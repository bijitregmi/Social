document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#edit-button').forEach((edit) => {

        // Event for each edit button
        edit.addEventListener('click', () => edit_post(`${edit.value}`, edit));
    });

    // Event for each like
    document.querySelectorAll('.like').forEach((like) => {

        const parent = like.closest('.wrapper');
        const post_id = parent.dataset.value;
        like.addEventListener('click', () => like_post(`${post_id}`, like));

    })
});

function edit_post(id, edit) {

    // Hide post details and display editbox
    const parent = edit.closest('.wrapper');
    const input = parent.querySelector('#edit-box');
    const post_content = parent.querySelector('.post-content');
    parent.querySelector('.post-body').style.display = 'none';
    parent.querySelector('.post-details').style.display = 'none';
    parent.querySelector('.post-edit-form').style.display = 'block';
    input.value = post_content.innerText.trim();


    // Add even listener to save button
    const save = parent.querySelector('#save-btn');
    save.addEventListener('click', () => edit_save(`${id}`, `${input.value}`, edit), {once: true});
}

async function edit_save(id, content, edit) {

    // Get csrftoken and save edit
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    try {
        const response = await fetch(`/edit/${id}`, {
            headers: {"X-CSRFToken": `${csrftoken}` },
            method: 'PUT',
            body: JSON.stringify({
                content: `${content}`
            })
        });
        const data = await response.json();
        console.log(data);

        // Display edited post
        const parent = edit.closest('.wrapper');
        parent.querySelector('.post-content').innerText = `${data.content}`
        parent.querySelector('.post-edit-form').style.display = 'none';
        parent.querySelector('.post-body').style.display = 'block';
        parent.querySelector('.post-details').style.display = 'block';
        

    }

    // Error handling
    catch (error) {
        console.log(error)
    }
}


// Like or unlike post
async function like_post(id, like) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (like.innerText === "Like"){
        try {
            const response = await fetch(`/like/${id}`, {
                headers: {"X-CSRFToken": `${csrftoken}` },
                method: 'PUT',
                body: JSON.stringify({
                    liked: true 
                })
            });
            const data = await response.json();
            console.log(data);
            const parent = like.closest('.wrapper');
            const amount = parent.querySelector('#likes-amount');
            amount.innerText = `Likes: ${data.likes}`;
            like.innerText = 'Unlike';
        }
        catch(error) {
            console.log(error)
        }
    }

    // For unlike
    else {
        try {
            const response = await fetch(`/like/${id}`, {
                headers: {"X-CSRFToken": `${csrftoken}` },
                method: 'PUT',
                body: JSON.stringify({
                    liked: false 
                })
            });
            const data = await response.json();
            console.log(data);
            const parent = like.closest('.wrapper');
            const amount = parent.querySelector('#likes-amount');
            amount.innerHTML = `Likes: ${data.likes}`;
            like.innerText = 'Like';
        }
        catch(error) {
            console.log(error)
        }
    }
}