import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import {
    Button,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Input,
    Link,
    Text,
} from '@chakra-ui/react';
import { Routes } from '../../routes/routes.types';
import { Link as ReactLink, useNavigate } from 'react-router-dom';
import styles from './login.module.scss';
import { login } from '../../api/auth.api';
import { useDispatch } from 'react-redux';
import { setUser } from '../../store/core/core.actions';
import { ValidationError } from '../../models/ValidationError';

type FormType = {
    username: string;
    password: string;
};

const Login = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const {
        handleSubmit,
        register,
        formState: { errors, isSubmitting },
    } = useForm<FormType>();
    const [error, setError] = useState<string | null>(null);

    const onSubmit = ({ username, password }: FormType) => {
        setError(null);
        login(username, password)
            .then(user => {
                dispatch(setUser(user));
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
                <FormControl isInvalid={!!errors.password}>
                    <FormLabel htmlFor="password">Password</FormLabel>
                    <Input
                        id={'password'}
                        type={'password'}
                        placeholder={'Password'}
                        {...register('password', { required: 'This field is required' })}
                    />
                    <FormErrorMessage>
                        {errors.password && errors.password.message}
                    </FormErrorMessage>
                </FormControl>
                <Button mt={4} colorScheme="blue" isLoading={isSubmitting} type="submit">
                    Login
                </Button>
            </form>
            {error && <Text color={'red.500'}>{error}</Text>}
            <Link as={ReactLink} to={Routes.REGISTER}>
                Create an account
            </Link>
        </div>
    );
};

export default Login;
