
export default AuthContext;

import { createContext, useState, useContext, useEffect } from 'react';
import { getCurrentUser } from 'aws-amplify/auth';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkAuth(); // 초기 인증 상태 확인
    }, []);

    const checkAuth = async () => {
        setLoading(true); // 로딩 시작
        try {
            const storedUserInfo = localStorage.getItem('userInfo');
            if (storedUserInfo) {
                const parsedUserInfo = JSON.parse(storedUserInfo);
                setUser(parsedUserInfo);
            }

            // Cognito 세션 확인
            const currentUser = await getCurrentUser();
            if (currentUser) {
                const response = await fetch(
                    `http://localhost:5002/api/auth/user/${currentUser.userId}`,
                    {
                        method: 'GET',
                        headers: { 'Content-Type': 'application/json' }
                    }
                );

                if (response.ok) {
                    const { user: userData } = await response.json();
                    const updatedUser = {
                        ...userData,
                        sub: currentUser.userId
                    };
                    setUser(updatedUser);
                    localStorage.setItem('userInfo', JSON.stringify(updatedUser));
                }
            } else {
                throw new Error('No current user session.');
            }
        } catch (error) {
            console.error('인증 체크 에러:', error);
            setUser(null);
            localStorage.removeItem('userInfo');
        } finally {
            setLoading(false); // 로딩 완료
        }
    };

    const value = { user, setUser, loading, checkAuth };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children} {/* 로딩이 끝난 후에만 children 렌더링 */}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth는 AuthProvider 내부에서만 사용할 수 있습니다');
    }
    return context;
};

// export default AuthContext;