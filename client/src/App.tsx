import * as React from 'react';
import { Box, Grid } from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import { Router } from './routes/router';

export const App = () => (
    <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={3}>
            <ColorModeSwitcher justifySelf="flex-end" />
            <Router />
        </Grid>
    </Box>
);
