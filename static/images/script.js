
const tbody = document.getElementById('imagesTableBody');


fetch('/api/images').then(response => response.json()).then(images => setImages(images.images));

function setImages(images) {
    const imagesContainer = document.createElement('div');
    images.forEach(image => {
        const tr = document.createElement('tr');

        const tdName = document.createElement('td');
        const tdUrl = document.createElement('td');
        const tdDelete = document.createElement('td');

        const deleteButton = document.createElement('button');
        deleteButton.classList.add('delete-btn');
        deleteButton.textContent = 'X';
        tdDelete.appendChild(deleteButton);
        tdName.textContent = image;
        tdUrl.innerHTML = `<a href="/images/${image}" target="_blank">${image}</a>`;

        tr.appendChild(tdName);
        tr.appendChild(tdUrl);
        tr.appendChild(tdDelete);

        tbody.appendChild(tr);
    });
    document.body.appendChild(imagesContainer);
}

// <tbody id="imagesTableBody">
//    <tr>
//        <td>Cat.png</td>
//        <td><a href="https://sharefile.xyz/file.jpg" target="_blank">https://sharefile.xyz/file.jpg</a>
//        </td>
//        <td>
//            <button class="delete-btn">X</button>
//        </td>
//    </tr>
//    </tbody>