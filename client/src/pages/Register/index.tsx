import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import {
    Button,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Input,
    InputGroup,
    InputRightElement,
    Link,
    Select,
    Text,
} from '@chakra-ui/react';
import { Routes } from '../../routes/routes.types';
import { Link as ReactLink, useNavigate } from 'react-router-dom';
import styles from './register.module.scss';
import { LanguagesValues } from '../../models/languages';
import { register as registerApi } from '../../api/auth.api';
import { useDispatch } from 'react-redux';
import { setUser } from '../../store/core/core.actions';
import { ValidationError } from '../../models/ValidationError';

type FormType = {
    username: string;
    password: string;
    lang: string;
};

const Register = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const {
        handleSubmit,
        register,
        formState: { errors, isSubmitting },
    } = useForm<FormType>();
    const [error, setError] = useState<string | null>(null);
    const [showPassword, setShowPassword] = useState<boolean>(false);

    const onSubmit = ({ username, lang, password }: FormType) => {
        setError(null);
        registerApi(username, password, lang)
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
                    <InputGroup>
                        <Input
                            id={'password'}
                            type={showPassword ? 'text' : 'password'}
                            placeholder={'Password'}
                            {...register('password', { required: 'This field is required' })}
                        />
                        <InputRightElement width="4.5rem">
                            <Button
                                h="1.75rem"
                                size="sm"
                                onClick={() => setShowPassword(!showPassword)}
                            >
                                {showPassword ? 'Hide' : 'Show'}
                            </Button>
                        </InputRightElement>
                    </InputGroup>
                    <FormErrorMessage>
                        {errors.password && errors.password.message}
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
                            <option value={value}>{prop}</option>
                        ))}
                    </Select>
                    <FormErrorMessage>{errors.lang && errors.lang.message}</FormErrorMessage>
                </FormControl>
                <Button mt={4} colorScheme="blue" isLoading={isSubmitting} type="submit">
                    Register
                </Button>
                {error && <Text color={'red.500'}>{error}</Text>}
            </form>
            <Link as={ReactLink} to={Routes.LOGIN}>
                Already have an account?
            </Link>
        </div>
    );
};

export default Register;
