// frontend/src/components/UserList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserList() {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        axios.get('/api/v1/users/')
            .then(response => setUsers(response.data))
            .catch(error => console.error('Erro ao buscar usuários:', error));
    }, []);

    return (
        <div>
            <h2>Lista de Usuários</h2>
            <ul>
                {users.map(user => (
                    <li key={user.id}>{user.username}</li>
                ))}
            </ul>
        </div>
    );
}

export default UserList;