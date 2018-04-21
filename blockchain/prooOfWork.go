package main

import (
	"math/big"
	"bytes"
)

const targetBits = 24

// 工作证明
type ProofOfWord struct {
	block  *Block
	target *big.Int
}

// 解析data
func (pow *ProofOfWord) prepareData(nonce int) []byte {
	data := bytes.Join([][]byte{
		pow.block.PreHash,
		pow.block.Data,
		IntToHex(pow.block.Timestamp),
		IntToHex(int64(targetBits)),
		IntToHex(int64(nonce)),
	}, []byte{})
	return data
}

func NewProoOfWord(block *Block) *ProofOfWord {
	target := big.NewInt(1)
	target.Lsh(target, uint(256-targetBits))
	pow := &ProofOfWord{block, target}
	return pow
}

