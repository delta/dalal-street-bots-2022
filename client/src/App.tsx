import * as React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import {
    ChakraProvider,
    Box,
    Text,
    VStack,
    Grid,
    theme,
    Heading,
    FormControl,
    FormLabel,
    Input,
    Button
} from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import { Logo } from './Logo';

export const App = () => (
    <ChakraProvider theme={theme}>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<HomePage />} />
            </Routes>
            <Routes>
                <Route path="/login" element={<Login />} />
            </Routes>
        </BrowserRouter>
    </ChakraProvider>
);

const HomePage = () => {
    return (
        <Box textAlign="center" fontSize="xl">
            <Grid minH="100vh" p={3}>
                <ColorModeSwitcher justifySelf="flex-end" />
                <VStack spacing={8}>
                    <Logo h="40vmin" pointerEvents="none" />
                    <Text>Dalal To The Moon</Text>
                    <Link to="/login">
                        <Button
                            rounded="none"
                            colorScheme="green"
                            w={['full', 'auto']}
                        >
                            Login
                        </Button>
                    </Link>
                </VStack>
            </Grid>
        </Box>
    );
};

const Login = () => {
    return (
        <Box
            w={['full', 'md']}
            p={[8, 10]}
            mt={[20, '10vh']}
            border={['none', '1px']}
            borderColor={['', 'gray']}
            borderRadius={15}
        >
            <VStack spacing={4} align="flex-start" w="full">
                <VStack>
                    <Heading>Login</Heading>
                    <Text>Enter e-mail and password</Text>
                </VStack>
                <FormControl>
                    <FormLabel>E-mail address</FormLabel>
                    <Input rounded="none" variant="filled" />
                </FormControl>
                <FormControl>
                    <FormLabel>Password</FormLabel>
                    <Input rounded="none" variant="filled" type="password" />
                </FormControl>
                <Button rounded="none" colorScheme="green">
                    Login
                </Button>
                <Link to="/">
                    <Button rounded="none" colorScheme="orange">
                        back
                    </Button>
                </Link>
            </VStack>
        </Box>
    );
};
