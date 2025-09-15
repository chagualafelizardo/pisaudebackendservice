$(document).ready(function () {
    if (window.location.pathname.includes("roles")) {
        loadRoles();

        $('#roleForm').on('submit', async function (e) {
            e.preventDefault();
            const id = $('#roleId').val();
            const description = $('#roleName').val();

            const method = id ? 'put' : 'post';
            const url = id ? `/api/role/${id}` : '/api/role';

            try {
                await $.ajax({ url, method, contentType: "application/json", data: JSON.stringify({ description }) });
                $('#roleForm')[0].reset();
                $('#roleId').val('');
                loadRoles();
            } catch (err) {
                alert('Error saving role.');
            }
        });

        $('#cancelEdit').click(function () {
            $('#roleForm')[0].reset();
            $('#roleId').val('');
        });
    }
});

async function loadRoles() {
    try {
        const res = await $.get('/api/role');
        const roles = res;
        const tbody = $('#rolesTableBody');
        tbody.empty();

        roles.forEach(role => {
            tbody.append(`
                <tr>
                    <td>${role.id}</td>
                    <td>${role.description}</td>
                    <td>
                        <button class="btn btn-sm btn-warning" onclick="editRole(${role.id}, '${role.description}')">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteRole(${role.id})">Delete</button>
                    </td>
                </tr>
            `);
        });
    } catch (err) {
        alert('Error loading roles.');
    }
}

async function deleteRole(id) {
    if (!confirm('Delete this role?')) return;
    try {
        await $.ajax({ url: `/api/role/${id}`, type: 'DELETE' });
        loadRoles();
    } catch (err) {
        alert('Error deleting role.');
    }
}

function editRole(id, description) {
    $('#roleId').val(id);
    $('#roleName').val(description);
}
