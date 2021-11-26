import React, { useEffect, useState } from 'react';
import { SendMessage } from './components/SendMessage/SendMessage';
import styles from './chat.module.scss';
import { getChat, getChats } from '../../api/chat.api';
import { Room } from '../../models/room';
import { Spinner } from '@chakra-ui/react';
import { Message } from '../../models/message';
import { ChatRoom } from './components/ChatRoom/ChatRoom';
import { LocalStorage } from '../../models/localstorage';

const Chat = () => {
    const [ws, setWs] = useState<WebSocket>();
    const [wsActive, setWSActive] = useState(false);
    const [room, setRoom] = useState<Room | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const userData = JSON.parse(localStorage.getItem(LocalStorage.USER) || '');
    const userId = userData.id;

    useEffect(() => {
        getChats()
            .then(res => getChat(res[0].id, userId))
            .then(res => {
                setRoom(res);
                setMessages(res.messages);
            });
    }, [userId]);

    useEffect(() => {
        if (room && !wsActive) {
            const webSocket = new WebSocket(`ws://localhost:5000/api/ws/${room.id}/${userId}`);
            webSocket.onopen = () => {
                setWs(webSocket);
                setWSActive(true);
            };

            webSocket.onmessage = ({ data }: { data: string }) => {
                setMessages((e: Message[]) => [...e, JSON.parse(data)]);
            };
        }
    }, [wsActive, room, userId]);

    useEffect(() => {
        return () => {
            ws?.close();
        };
    }, [ws]);

    const sendMessage = (message: string) => {
        ws?.send(message);
    };

    if (!room) {
        return (
            <Spinner
                thickness="4px"
                speed="0.65s"
                emptyColor="gray.200"
                color="blue.500"
                size="xl"
            />
        );
    }

    return (
        <div className={styles.container}>
            <SendMessage sendMessage={sendMessage} />
            <ChatRoom messages={messages!} userId={userId} />
        </div>
    );
};

export default Chat;
