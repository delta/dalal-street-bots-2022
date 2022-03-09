import { Box, Button, FormControl, FormLabel,Text, Grid, Heading, Input, Link, VStack } from '@chakra-ui/react';
import * as React from 'react';
import { useState } from 'react';
import {useNavigate} from 'react-router-dom';


export function LoggingIn(){
    const[email,setEmail]=useState("");
    const[password,setPassword]=useState("");
    const navigate = useNavigate();
    React.useEffect(() =>{
        if(localStorage.getItem('user-info'))
        {
            navigate("/login")
        }
    }, [])

   async function Login(){
        
        console.warn(email,password)
        let item = {email,password};
        let result =await fetch("localhost:3008/login",{
            method:'POST',
            headers:{
               "Content-Type":"application/json" ,
               "Accept":"application/json"
            },
            body:JSON.stringify(item)
        });
        result = await result.json();
        localStorage.setItem("user-info",JSON.stringify(result))
        navigate("/login") 
        
    }
    

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
                    <Input rounded="none" variant="filled" type ="text" placeholder="email" onChange={(e)=>setEmail(e.target.value)}/>
                </FormControl>
                <FormControl>
                    <FormLabel>Password</FormLabel>
                    <Input rounded="none" variant="filled" type="password" placeholder="password" onChange={(e)=>setPassword(e.target.value)}/>
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

}
