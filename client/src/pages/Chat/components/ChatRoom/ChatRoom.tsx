import React, { useEffect, useRef } from 'react';
import moment from 'moment';
import { Message } from '../../../../models/message';
import styles from './chat-room.module.scss';
import { Text } from '@chakra-ui/react';

const colorMap: { [prop: string]: string } = {};

type MessageProps = Message & {
    isOwnMessage: boolean;
};
const MessageComponent = ({
    text,
    user: { name, id },
    created_at,
    lang,
    isOwnMessage,
}: MessageProps) => {
    const getBackgroundColor = (userId: string) => {
        if (colorMap[userId]) return colorMap[userId];
        const randomColor = '#' + ((Math.random() * 0xffffff) << 0).toString(16);
        colorMap[userId] = randomColor;
        return randomColor;
    };

    return (
        <div className={styles.message} data-ownMessage={isOwnMessage}>
            <Text fontSize={'sm'} color={getBackgroundColor(id)} className={styles.title}>
                {isOwnMessage ? 'You' : name}
                <Text fontSize="xs" as="i">
                    {moment(created_at).format('hh:mm')}
                </Text>
            </Text>
            <Text className={styles.content}>
                {text}
                <Text fontSize="xs" as="i">
                    (Original message in {lang})
                </Text>
            </Text>
        </div>
    );
};


export const ChatRoom = ({ messages, userId }: { messages: Message[]; userId: string }) => {
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (ref?.current) {
            ref?.current?.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    return (
        <div className={styles.container}>
            {messages.map(message => (
                <MessageComponent
                    key={message.id}
                    isOwnMessage={message.user.id === userId}
                    {...message}
                />
            ))}
            <div ref={ref} style={{ visibility: 'hidden' }} />
        </div>
    );
};
