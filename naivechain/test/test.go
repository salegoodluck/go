package main


# 一句话总结：注意*与谁结合，如p *[5]int，*与数组结合说明是数组的指针；如p [5]*int，*与int结合，说明这个数组都是int类型的指针，是指针数组。
import "fmt"

func main() {

	a := [...]int{1, 2, 3, 4, 5}

	var p *[5]int = &a

	fmt.Println(*p, a)

	for index, value := range *p {

		fmt.Println(index, value)

	}

	var p2 [5]*int

	i, j := 10, 20

	p2[0] = &i

	p2[1] = &j

	for index, value := range p2 {

		if value != nil {

			fmt.Println(index, *value)

		} else {

			fmt.Println(index, value)

		}

	}

}
