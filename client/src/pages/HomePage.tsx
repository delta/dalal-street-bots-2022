import { Button } from '@chakra-ui/button';
import { Box, Grid, VStack ,Text, Link} from '@chakra-ui/layout';
import * as React from 'react';
import { ColorModeSwitcher } from '../ColorModeSwitcher';
import { Logo } from '../Logo';

export const HomePage = () => {
    return (
      
        <Box textAlign="center" fontSize="xl" alignItems="stretch">
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
