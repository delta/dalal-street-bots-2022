import * as React from 'react';
import {
    Box,
    Button,
    FormLabel,
    Grid,
    Heading,
    Input,
    VStack,
    Center
} from '@chakra-ui/react';
import { Link } from 'react-router-dom';
import { ColorModeSwitcher } from '../ColorModeSwitcher';
import { useState } from 'react';

export const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const submitForm = () => {
        console.log(email, password);
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
                                <Heading>Login</Heading>
                            </VStack>
                            <form
                                onSubmit={(e) => {
                                    e.preventDefault();
                                    submitForm();
                                }}
                            >
                                <FormLabel>E-mail address</FormLabel>
                                <Input
                                    rounded="none"
                                    variant="filled"
                                    required={true}
                                    onChange={(e) => setEmail(e.target.value)}
                                />
                                <FormLabel>Password</FormLabel>
                                <Input
                                    rounded="none"
                                    variant="filled"
                                    type="password"
                                    onChange={(e) =>
                                        setPassword(e.target.value)
                                    }
                                    required={true}
                                />
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
