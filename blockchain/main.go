package main

import (
	"fmt"
)

// 执行创世区块
func main() {
	blockChain := NewBlockChain()
	blockChain.addBlock("hello 1")
	blockChain.addBlock("hello 2")
	for _, block := range blockChain.blocks {
		fmt.Printf("Phash: %x\n", block.PreHash)
		fmt.Printf("Data: %s\n", block.Data)
		fmt.Printf("Hash: %x\n", block.Hash)
		fmt.Println()
	}
}
