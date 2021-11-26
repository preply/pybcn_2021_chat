import React, { useEffect } from 'react';
import { SendMessage } from './components/SendMessage/SendMessage';
import styles from './chat.module.scss';
import { getChats } from '../../api/chat.api';

const Chat = () => {
    useEffect(() => {
        getChats().then(res => console.log(res));
    }, []);

    const sendMessage = (message: string) => {
        console.log(message);
    };
    return (
        <div className={styles.container}>
            <SendMessage sendMessage={sendMessage} />
        </div>
    );
};

export default Chat;
