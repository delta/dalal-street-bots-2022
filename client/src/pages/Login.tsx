import { Box, Button, FormControl, FormLabel,Text, Grid, Heading, Input, Link, VStack } from '@chakra-ui/react';
import * as React from 'react';

export const Login = () => {
    return (
      <div>
      <Grid container direction="column" alignItems="center"justify="center">
        <Box
            p={[10, 10]}
            mt={[50, '10vh']}
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
        </Grid>
        </div>
         
       
    );
};