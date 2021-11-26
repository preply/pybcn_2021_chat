import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import {
    Button,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Input,
    Select,
    Text,
} from '@chakra-ui/react';
import { Routes } from '../../routes/routes.types';
import { useNavigate } from 'react-router-dom';
import styles from './register.module.scss';
import { LanguagesValues } from '../../models/languages';
import { register as registerApi } from '../../api/auth.api';
import { ValidationError } from '../../models/ValidationError';
import { LocalStorage } from '../../models/localstorage';

type FormType = {
    username: string;
    lang: string;
};

const Register = () => {
    const navigate = useNavigate();
    const {
        handleSubmit,
        register,
        formState: { errors, isSubmitting },
    } = useForm<FormType>();
    const [error, setError] = useState<string | null>(null);

    const onSubmit = ({ username, lang }: FormType) => {
        setError(null);
        registerApi(username, lang)
            .then(({ data }) => {
                localStorage.setItem(LocalStorage.USER, JSON.stringify(data));
                navigate(Routes.CHAT);
            })
            .catch((error: ValidationError) =>
                setError(error?.detail?.length ? error.detail[0].msg : 'Something went wrong'),
            );
    };

    return (
        <div className={styles.container}>
            <form onSubmit={handleSubmit(onSubmit)}>
                <FormControl isInvalid={!!errors.username}>
                    <FormLabel htmlFor="username">Username</FormLabel>
                    <Input
                        id={'username'}
                        placeholder={'Username'}
                        {...register('username', { required: 'This field is required' })}
                    />
                    <FormErrorMessage>
                        {errors.username && errors.username.message}
                    </FormErrorMessage>
                </FormControl>
                <FormControl isInvalid={!!errors.lang}>
                    <FormLabel htmlFor={'lang'}>Language </FormLabel>
                    <Select
                        id={'lang'}
                        placeholder={'Language'}
                        {...register('lang', { required: 'This field is required' })}
                    >
                        {Object.entries(LanguagesValues).map(([prop, value]) => (
                            <option key={value} value={value}>
                                {prop}
                            </option>
                        ))}
                    </Select>
                    <FormErrorMessage>{errors.lang && errors.lang.message}</FormErrorMessage>
                </FormControl>
                <Button mt={4} colorScheme="blue" isLoading={isSubmitting} type="submit">
                    Register
                </Button>
                {error && <Text color={'red.500'}>{error}</Text>}
            </form>
        </div>
    );
};

export default Register;
