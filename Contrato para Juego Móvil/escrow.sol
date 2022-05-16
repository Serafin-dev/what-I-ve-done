// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Address.sol";
import "@openzeppelin/contracts/finance/PaymentSplitter.sol";

contract Mescrow is Ownable, PaymentSplitter{
    using Address for address payable;

    event Deposited(address indexed payee, uint256 weiAmount);
    event Withdrawn(address indexed payee, uint256 weiAmount);
    event NewPlayerRegistered(address indexed player);
    
    mapping(address => uint256) private _deposits;
    mapping(address => uint256) private _released;

    // Payment splitter variables
    uint256 private _totalShares;
    uint256 private _totalReleased;
    address[] public players;

    // Cost of ONE game
    uint256 public gamePrice;
    
    // Active users
    mapping (address => bool) activeUsers;

    /** 
    JS virtual machine: 1000000000000000000,["0x5B38Da6a701c568545dCfcB03FcB875f56beddC4","0xCA35b7d915458EF540aDe6068dFe2F44E8fa733c","0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB"],[300,400,300]
    Ethereum Ropsten testnet:
    -Deployment parameters: 100000000000000,["0x1A2e48b8daD8A9f2e6A3d41cEBab1214726dbD93","0x75FCE093358474B56cfDeBA7FF798B6Bc014fCda","0x7a00eddAC1100C429213E508A24951DDde27A930"],[300,400,300]
    -Contract ADDRESS: "0x78FB58C86460FFcF409FFFB2ce1B52a0f59470a8"
    */
    constructor(uint256 price, address[] memory payees_, uint256[] memory shares_) PaymentSplitter(payees_, shares_) payable {
        // Set the cost of a room
        gamePrice = price;
    }
    // Prevent Reentrancy 
    bool locked;
    modifier noReentrancy() {
        require(
            !locked,
            "Reentrant call."
        );
        locked = true;
        _;
        locked = false;
    }
    // check if an account is already suscribed
    modifier registeredPlayer(){
        require (activeUsers[msg.sender] == true, "You need to register first!");
        _;
    }
    // ckeck if it is a Master share holder
    modifier onlyMasterPayee() {
        require(shares(msg.sender) > 0, "PaymentSplitter: account has no shares");
        _;
    }
    function changeGamePrice(uint256 newValue) public onlyOwner{
        gamePrice = newValue;
    }
    // Get Player Balances 
    function depositsOf(address player) public view returns (uint256) {
        return _deposits[player];
    }
    // User: Register Player
    function register(address newPlayer) private {
        activeUsers[newPlayer] = true;
        emit NewPlayerRegistered(newPlayer);
    }
    // charge comission
    function chargeMasterComission(uint256 amount) private {
        _deposits[owner()] += amount * 3 / 100;
    }
    // get master commission
    function masterCommission(uint256 payment)public pure returns(uint256){
        return payment * 3 / 100;
    }
    // Pay subscription. This is a MUST to register as an active Player.
    function paySubscription(address account) public payable {
        uint256 amount = msg.value;

        // Ckeck if the amount for the subscription is ok
        require (amount >= 1 ether, "To register you need to pay at least 1 ether!");
        require (!activeUsers[account],"You are already registered");

        // Update player balance
        _deposits[account] += amount - masterCommission(amount);
        // Update Master Balance
        _deposits[owner()] += masterCommission(amount);
        // Register player 
        register(account);
        // Emit Balance update Event
        emit Deposited(account, amount);
    }
    // Make a deposit. You have to be a registered player first.
    function deposit(address player) public payable registeredPlayer{
        uint256 amount = msg.value;
        // update player balance
        _deposits[player] += amount - masterCommission(amount);
        // charge 3% : Master comission
        _deposits[owner()] += masterCommission(amount);
        emit Deposited(player, amount);
    }
    // Update winner balance
    function payToWinner(address _winner) private {
        _deposits[_winner] += gamePrice *  3;
    }
    // Update Loser Balance
    function discountLosers(address[] memory _losers) private {
        for (uint i=0; i > _losers.length; i++) {
            _deposits[_losers[i]] -= gamePrice;
        }
    }
    // After a game ended, update balances of all the players
    function updateBalancesAfterGame(address[] memory _losers, address winner) public onlyOwner {
        //verificar que la partida sea real(a ampliar)
        discountLosers(_losers);
        payToWinner(winner);
    }
    // withdraw funds to personal wallet
    function withdraw(address payable player) public registeredPlayer noReentrancy {
        require(_deposits[player] > 0, "You have no funds.");
        require(player != owner(), "You can't withdraw this way. You must release.");

        uint256 payment = _deposits[player];
        _deposits[player] = 0;
        player.sendValue(payment);

        emit Withdrawn(player, payment);
    }
    function masterReleased(address account) public view returns (uint256) {
        return _released[account];
    }
    function masterTotalReleased() public view returns (uint256) {
        return _totalReleased;
    }
    // Admin: Withdraw funds based on share holders - Master associates only
    function release(address payable account) public override onlyMasterPayee{

        uint256 totalReceived = _deposits[owner()] + masterTotalReleased();
        uint256 payment = (totalReceived * shares(account)) / totalShares() - masterReleased(account);

        require(payment != 0, "PaymentSplitter: account is not due payment");

        _released[account] += payment;
        _totalReleased += payment;
        _deposits[owner()] -= payment;

        account.sendValue(payment);
        emit PaymentReleased(account, payment);
    }  
}

