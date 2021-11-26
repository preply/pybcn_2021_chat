import * as React from 'react';
import { Box, Grid } from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import { Router } from './routes/router';
import { useEffect } from 'react';
import { getUser } from './api/user.api';
import { useDispatch } from 'react-redux';
import { setUser } from './store/core/core.actions';

export const App = () => {
    const dispatch = useDispatch();

    const getUserData = async () => {
        const user = await getUser();
        !!user && dispatch(setUser(user));
    };

    useEffect(() => {
        getUserData();
    }, [dispatch, getUserData]);

    return (
        <Box textAlign="center" fontSize="xl">
            <Grid minH="100vh" p={3}>
                <ColorModeSwitcher justifySelf="flex-end" />
                <Router />
            </Grid>
        </Box>
    );
};
