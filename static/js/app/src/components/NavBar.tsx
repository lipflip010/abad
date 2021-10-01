import React from 'react';
import './NavBar.scss'

const NavBar = () => {
    return (
        <div>
            <div className="NavBar">
                <a href="/" className="NavBar__Item">Home</a>
                <a href="/storage" className="NavBar__Item">Storage</a>
                <a href="/commands" className="NavBar__Item">Commands</a>
            </div>
        </div>
    );
};

export default NavBar;