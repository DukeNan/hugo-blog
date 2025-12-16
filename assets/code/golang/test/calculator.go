package calculator

import (
	"errors"
	"math"
)

// Add 加法运算
func Add(a, b int) int {
	return a + b
}

// Subtract 减法运算
func Subtract(a, b int) int {
	return a - b
}

// Multiply 乘法运算
func Multiply(a, b int) int {
	return a * b
}

// Divide 除法运算
func Divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, errors.New("division by zero")
	}
	return a / b, nil
}

// IsPrime 判断是否为质数
func IsPrime(n int) bool {
	if n <= 1 {
		return false
	}
	if n <= 3 {
		return true
	}
	if n%2 == 0 || n%3 == 0 {
		return false
	}
	for i := 5; i*i <= n; i += 6 {
		if n%i == 0 || n%(i+2) == 0 {
			return false
		}
	}
	return true
}

// Factorial 计算阶乘
func Factorial(n int) int {
	if n < 0 {
		return -1
	}
	if n == 0 {
		return 1
	}
	result := 1
	for i := 1; i <= n; i++ {
		result *= i
	}
	return result
}

// Sqrt 计算平方根
func Sqrt(x float64) (float64, error) {
	if x < 0 {
		return 0, errors.New("negative number")
	}
	return math.Sqrt(x), nil
}

