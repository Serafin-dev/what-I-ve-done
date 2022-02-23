const { ethers } = require("ethers");

export const loadContract = async () => {
	const NERDISH_CONTRACT = await new ethers.Contract(contractAddress, window.abi, provider);   
    console.log(NERDISH_CONTRACT);
}

export const mintNFT = async (amount, options, NERDISH_CONTRACT) => {
    
    //error handling
    if (amount > 100 || amount <= 0) { 
        return {
            success: false,
            status: "❗Ingresa un valor del 1 al 100!",
        }
    }
    //set up your Ethereum transaction
    const transactionParameters = {
        to: contractAddress, // Required except during contract publications.
        from: window.ethereum.selectedAddress, // must match user's active address.
		'data': window.NERDISH_CONTRACT.mintNERD(10, options).encodeABI() //make call to NFT smart contract 
    };
  
    //sign transaction via Metamask
    try {
        const txHash = await window.ethereum
            .request({
                method: 'eth_sendTransaction',
                params: [transactionParameters],
            });
        return {
            success: true,
            status: "✅ Quitter! Mirá tu transacción en Etherscan: https://ropsten.etherscan.io/tx/" + txHash
        }
    } catch (error) {
        return {
            success: false,
            status: "😥 Algo impredecible salió mal " + error.message
        }
    }
}