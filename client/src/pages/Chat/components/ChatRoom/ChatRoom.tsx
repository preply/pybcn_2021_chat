import React from 'react';
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
        <div
            className={styles.message}
            style={{ background: getBackgroundColor(id) }}
            data-ownMessage={isOwnMessage}
        >
            <Text fontSize={'sm'}>
                {isOwnMessage ? 'You' : name} {moment(created_at).format('hh:mm')}
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

export const ChatRoom = ({ messages, userId }: { messages: Message[]; userId: string }) => (
    <div className={styles.container}>
        {messages.map(msg => typeof msg === 'string' ? JSON.parse(msg) : msg).map((message, i) => (
            <MessageComponent key={i} {...message} isOwnMessage={message.user.id === userId} />
        ))}
    </div>
);
