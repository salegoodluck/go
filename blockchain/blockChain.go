package main

import (
	"strconv"
	"bytes"
	"crypto/sha256"
	"time"
)

// 区块数据结构
type Block struct {
	Timestamp int64
	Data      []byte
	PreHash   []byte
	Hash      []byte
}

// 创建hash
func (block *Block) MakeHash() {
	blockTime := []byte(strconv.FormatInt(block.Timestamp, 10))
	str := bytes.Join([][]byte{block.PreHash, block.Data, blockTime}, []byte{})
	hash := sha256.Sum256(str)
	block.Hash = hash[:]
}

// 区块链数据结构
type BlockChain struct {
	blocks []*Block
}

// 入库数据
func (blockchain *BlockChain) addBlock(data string) {
	preBlock := blockchain.blocks[len(blockchain.blocks)-1]
	newBlock := MakeBlock(data, preBlock.Hash)
	blockchain.blocks = append(blockchain.blocks, newBlock)
}

// 创建区块
func MakeBlock(data string, preHash []byte) *Block {
	nowTime := time.Now().Unix()
	block := &Block{nowTime, []byte(data), preHash, []byte{}}
	block.MakeHash()
	return block
}

// 创建新的区块链
func NewBlockChain() *BlockChain {
	block := MakeBlock("hello blockChain", []byte{})
	return &BlockChain{[]*Block{block}}
}