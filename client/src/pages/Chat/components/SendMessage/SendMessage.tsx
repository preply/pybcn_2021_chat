import React from 'react';
import { Button, FormControl, FormLabel, Input } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import styles from './sendMesssages.module.scss';

type Form = {
    message: string;
};

export const SendMessage = ({ sendMessage }: { sendMessage: (message: string) => void }) => {
    const { handleSubmit, reset, register } = useForm<Form>();
    const onSubmit = ({ message }: Form) => {
        sendMessage(message);
        reset();
    };
    return (
        <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
            <FormControl>
                <FormLabel htmlFor={'message'}>Message</FormLabel>
                <Input id={'message'} placeholder={'Message here...'} {...register('message')} />
            </FormControl>
            <Button mt={4} colorScheme="blue" type="submit">
                Send
            </Button>
        </form>
    );
};
