import * as React from 'react';
import {
    Box,
    Button,
    FormLabel,
    FormControl,
    Grid,
    Heading,
    Input,
    VStack,
    Center
} from '@chakra-ui/react';
import { Link } from 'react-router-dom';
import { ColorModeSwitcher } from '../ColorModeSwitcher';
import { useState } from 'react';
import { axiosInstance } from '../utils/axios';

export const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const submitForm = async () => {
        // console.log(email, password);

        try {
            const resp = await axiosInstance.post('/auth/login', {
                email,
                password
            });
            console.log(resp.data);
        } catch (error: any) {
            console.log(error);
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                console.log(error.response.data);
                console.log(error.response.status);

                if (error.response.status === 401) {
                    localStorage.removeItem('token');
                }
            } else if (error.request) {
                // The request was made but no response was received
                // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                // http.ClientRequest in node.js
                console.log(error.request);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.log('Error', error.message);
            }
            console.log(error.config);
        }
    };

    return (
        <div>
            <ColorModeSwitcher justifySelf="flex-end" />
            <Grid
                container
                direction="column"
                alignItems="center"
                justify="center"
            >
                <Center>
                    <Box
                        p={[10, 10]}
                        mt={[50, '10vh']}
                        border={['none', '1px']}
                        borderColor={['', 'gray']}
                        borderRadius={15}
                        w="container.sm"
                    >
                        <VStack spacing={4} align="flex-start" w="full">
                            <VStack>
                                <Heading fontSize={'5xl'}>Login</Heading>
                                {/* <p>Login with server creds</p> */}
                            </VStack>
                            <form
                                onSubmit={(e) => {
                                    e.preventDefault();
                                    submitForm();
                                }}
                                style={{ width: '100%' }}
                            >
                                <FormControl>
                                    <FormLabel htmlFor="email">
                                        Email address
                                    </FormLabel>
                                    <Input
                                        id="email"
                                        type="email"
                                        required={true}
                                        onChange={(e) =>
                                            setEmail(e.target.value)
                                        }
                                    />
                                </FormControl>
                                <br />
                                <FormControl>
                                    <FormLabel htmlFor="password">
                                        Password
                                    </FormLabel>
                                    <Input
                                        id="password"
                                        type="password"
                                        required={true}
                                        onChange={(e) =>
                                            setPassword(e.target.value)
                                        }
                                    />
                                </FormControl>
                                <Button
                                    rounded="none"
                                    colorScheme="green"
                                    type="submit"
                                >
                                    Login
                                </Button>
                                <Link to="/">
                                    <Button
                                        rounded="none"
                                        colorScheme="orange"
                                        m={[0, 5]}
                                    >
                                        Back
                                    </Button>
                                </Link>
                            </form>
                        </VStack>
                    </Box>
                </Center>
            </Grid>
        </div>
    );
};
