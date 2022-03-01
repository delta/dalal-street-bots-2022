import * as React from 'react';
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import {
    ChakraProvider,
   
    theme,
  
} from '@chakra-ui/react';

import  {Login}  from './pages/Login'
import { HomePage } from './pages/HomePage';

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




