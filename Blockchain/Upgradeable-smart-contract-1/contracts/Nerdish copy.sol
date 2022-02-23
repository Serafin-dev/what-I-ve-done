// SPDX-License-Identifier: MIT
pragma solidity ^0.6.2;

import "@openzeppelin/contracts-ethereum-package/contracts/Initializable.sol";
import "@openzeppelin/contracts-ethereum-package/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts-ethereum-package/contracts/payment/PaymentSplitter.sol";
import "@openzeppelin/contracts-ethereum-package/contracts/access/Ownable.sol";

contract NerdsProject is Initializable, ERC721UpgradeSafe, PaymentSplitterUpgradeSafe, OwnableUpgradeSafe{

        //payees = ["0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1","0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"]
        //shares_ = [50, 50]
        //shares_ = [50, 50]

        //almaceno en un array privado las dos direcciones de metamask.
        address[] splitAddresses;
        uint public constant PRICE = 0.04 ether;
        uint public constant MAX_SUPPLY = 10000;
        uint public constant MAX_MINT_AMOUNT = 100;
        
        //Buyers with their respective NERD id
        mapping (address => uint) public buyerToNerd;
        
        //Contract administrators
        mapping (address => bool ) private ownerByAddress;
        address[] private admins;


        //admin 
        event pullSuccess(string msj);
        event printAdmins(address[] admins);

        //constructor
        function initialize( string memory _name, string memory _symbol, 
                             address[] memory _payees, uint256[] memory _shares) 
                             public payable initializer{

                __ERC721_init(_name, _symbol);   
                __PaymentSplitter_init(_payees, _shares);
                __Ownable_init(); 
                admins = _payees;
                for(uint i = 0; i < admins.length; i++){
                        ownerByAddress[admins[i]] = true;
                }
                emit printAdmins(admins);
        }

        modifier onlyAdmins(){
                require(ownerByAddress[msg.sender] == true);
                _;
        }
        // Minting
        function mintNerd (uint _amount) public payable {
                require(_amount != 0 && _amount <= MAX_MINT_AMOUNT, "Cantidad de NERDS incorrecta");
                //require(msg.value >= PRICE.mul(_amount), "Cantidad de ether incorrecto");
                
                for (uint _id = totalSupply() + 1; _id <= _amount; _id ++){
                        _mint(msg.sender, _id);
                        buyerToNerd[msg.sender] = _id;
                }
        }

        // Pull Ether from the contracto to an admin's account
        function pullPayment () public onlyAdmins {
                emit pullSuccess("pull success");
                release(msg.sender);
        }

}       

