import React, {ReactNode} from 'react';
type DefaultPageProps = {
    children: ReactNode
}

const DefaultPage = ({children}: DefaultPageProps) => {
    return (
        <div>
            {children}
        </div>
    );
};

export default DefaultPage;