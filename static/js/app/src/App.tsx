import React from 'react';
import logo from './logo.svg';
import './App.css';
import DefaultPage from "./pages/DefaultPage";
import NavBar from "./components/NavBar";
import useDocumentTitle from "./hooks/useDocumentTitle";

function App() {
    useDocumentTitle('abad: philipp-2T460S')
    return (
        <DefaultPage>
            <NavBar/>
        </DefaultPage>
    );
}

export default App;
