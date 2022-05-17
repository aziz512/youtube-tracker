import React from 'react';
import styled from 'styled-components';
import Dropdown from './DropdownMenu/Dropdown';

const people = [
  { name: 'Edmon Wong', link: 'https://github.com/Edmond120' },
  { name: 'Aziz Yokubjonov', link: 'https://github.com/aziz512' },
  { name: 'Haitham Alnajar', link: 'https://www.google.com' },
  { name: 'Yankang (Kyle) Xue', link: 'https://github.com/KanG98' },
  { name: 'Kamille Tipan', link: 'https://github.com/aziz512/youtube-tracker' },
];

const Navbar = () => {
  return (
    <Nav>
      <Logo href="">
        Video<span>Tube</span>
      </Logo>
      <Menu>
        <Dropdown people={people}></Dropdown>
        <MenuLink
          href="https://github.com/aziz512/youtube-tracker"
          target="_blank"
        >
          Our Work
        </MenuLink>
      </Menu>
    </Nav>
  );
};

export default Navbar;

const MenuLink = styled.a`
  padding: 1rem 2rem;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  color: #67bc98;
  transition: all 0.3s ease-in;
  font-size: 0.9rem;
  &:hover {
    color: #7b7fda;
  }
`;

const Nav = styled.div`
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  background: white;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
`;

const Logo = styled.a`
  padding: 1rem 0;
  color: #7b7fda;
  text-decoration: none;
  font-weight: 800;
  font-size: 1.7rem;
  span {
    font-weight: 300;
    font-size: 1.3rem;
  }
`;

const Menu = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  @media (max-width: 768px) {
    overflow: hidden;
    flex-direction: column;
    max-height: ${({ isOpen }) => (isOpen ? '300px' : '0')};
    transition: max-height 0.3s ease-in;
    width: 100%;
  }
`;
