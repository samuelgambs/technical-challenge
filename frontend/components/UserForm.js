// frontend/src/components/UserForm.js
import React, { useState } from 'react';
import axios from 'axios';

function UserForm() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        axios.post('/api/v1/users/', { username, email, password })
            .then(response => {
                console.log('Usuário criado:', response.data);
                // Limpar formulário ou redirecionar
            })
            .catch(error => console.error('Erro ao criar usuário:', error));
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <button type="submit">Criar Usuário</button>
        </form>
    );
}

export default UserForm;