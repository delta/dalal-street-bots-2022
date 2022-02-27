import * as React from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import {
    ChakraProvider,
    Box,
    Text,
    VStack,
    Grid,
    theme,
    Switch,
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
       <Box textAlign="center" fontSize="xl">
       <Grid minH="100vh" p={3}>
         <ColorModeSwitcher justifySelf="flex-end" />
         <VStack spacing={8}>
           <Logo h="40vmin" pointerEvents="none" />
           <Text>Dalal To The Moon</Text>
         </VStack>
       </Grid>
     </Box>
    <Router>
       <div>
         <nav>
           <ul>
             <li>
               <Link to="/">{Login}</Link>
             </li>
           </ul>
         </nav>
         <Switch>
           <Route path="/">
             <Login />
           </Route>
         </Switch>
       </div>
     </Router>   
   </ChakraProvider>
);

const Login=() =>{
  return (
      <Box
          w={['full','md']}
          p={[8,10]}
          mt={[20, '10vh']}
          border={['none','1px']}
          borderColor ={['','gray']}
          borderRadius={15}
          >
          <VStack 
              spacing={4}
              align ='flex-start'
              w='full'>
                  <VStack>
                      <Heading>Login</Heading>
                      <Text>Enter e-mail and password</Text>
                      </VStack>
                      <FormControl>
                          <FormLabel>
                              E-mail address
                          </FormLabel>
                          <Input rounded ='none' variant = 'filled'/>
                      </FormControl>
                      <FormControl>
                          <FormLabel>
                              Password
                          </FormLabel>
                          <Input rounded ='none' variant = 'filled' type ='password'/>
                      </FormControl>
                      <Button rounded ='none'
                      colorScheme='green'
                      w={['full','auto']}>
                          Login</Button>
                      
              </VStack>
      </Box>
  );
}





