// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/finance/PaymentSplitter.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract Nerdish is ERC721, ERC721Enumerable, ERC721URIStorage, PaymentSplitter, Ownable{
        using SafeMath for uint256;
        using Counters for Counters.Counter;
        Counters.Counter private _tokenIdCounter;

        //payees_ = ["0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1","0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"]
        //shares_ = [50, 50]
        
        uint public constant PRICE = 0.0003 ether;
        uint public constant MAX_SUPPLY = 10000;
        uint public constant MAX_MINT_AMOUNT = 100;
        
        //Buyers with their respective NERD id
        mapping (address => uint) public buyerToNerd;
        
        //Se almacenan ["cuenta : acciones"]
        mapping(address => uint256) private _shares;
        //Se almacenan las extracciones ["cuenta : valor de extracción"]
        mapping(address => uint256) private _released;
        
        //Lista de administradores
        address[] public admins;
        
        //Se almacenan ["cuenta : verdadero/falso"] Verdadero si "ES" y falso si figura en el mapping
        mapping (address => bool ) private ownerByAddress;
        
        event pullSuccess(string msj);

        constructor (address[] memory _payees, uint256[] memory shares) ERC721 ("Nerdish", "NERD") PaymentSplitter (_payees, shares)  payable {
                        
                     admins = _payees;
                     for(uint i = 0; i < admins.length; i++){ ownerByAddress[admins[i]] = true;}
        }
        
        modifier onlyAdmins(){
                require(ownerByAddress[msg.sender] == true);
                _;
        }
        
        // Minting
        function mintNerd (uint256 _amount) public payable {
                require(_amount != 0 && _amount <= MAX_MINT_AMOUNT, "Cantidad de NERDS incorrecta");
                require(msg.value >= PRICE.mul(_amount), "Cantidad de ether incorrecto");
             
                for (uint256 _id = _tokenIdCounter.current(); _id <= _amount; _id++){
                        _safeMint(msg.sender, _id);
                        buyerToNerd[msg.sender] = _id;
                        _tokenIdCounter.increment();
                        //_setTokenURI(tokenId, uri);
                }
        }
        
        // Pull Ether from the contract to an admin's account
        function pullPayment(address payable _account) public onlyAdmins{
                release(_account);
       }
       
        function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory)
        {
            return super.tokenURI(tokenId);
        }

         function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
            super._burn(tokenId);
        }
        function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721Enumerable) returns (bool)
        {
            return super.supportsInterface(interfaceId);
        }

        function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal override(ERC721, ERC721Enumerable)
        {
            super._beforeTokenTransfer(from, to, tokenId);
        }
}       
