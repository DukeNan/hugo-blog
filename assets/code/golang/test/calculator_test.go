package calculator

import (
	"fmt"
	"testing"
)

// TestAdd 基本的单元测试
func TestAdd(t *testing.T) {
	result := Add(2, 3)
	expected := 5
	if result != expected {
		t.Errorf("Add(2, 3) = %d; want %d", result, expected)
	}
}

// TestSubtract 使用子测试
func TestSubtract(t *testing.T) {
	t.Run("positive numbers", func(t *testing.T) {
		result := Subtract(10, 5)
		if result != 5 {
			t.Errorf("got %d, want 5", result)
		}
	})

	t.Run("negative result", func(t *testing.T) {
		result := Subtract(5, 10)
		if result != -5 {
			t.Errorf("got %d, want -5", result)
		}
	})
}

// TestDivide 测试带错误返回的函数
func TestDivide(t *testing.T) {
	// 正常情况
	result, err := Divide(10, 2)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != 5.0 {
		t.Errorf("Divide(10, 2) = %f; want 5.0", result)
	}

	// 除零错误
	_, err = Divide(10, 0)
	if err == nil {
		t.Error("expected error for division by zero, got nil")
	}
}

// TestIsPrime 表格驱动测试（推荐方式）
func TestIsPrime(t *testing.T) {
	testCases := []struct {
		name     string
		input    int
		expected bool
	}{
		{"prime 2", 2, true},
		{"prime 3", 3, true},
		{"prime 5", 5, true},
		{"prime 7", 7, true},
		{"prime 11", 11, true},
		{"not prime 1", 1, false},
		{"not prime 4", 4, false},
		{"not prime 6", 6, false},
		{"not prime 8", 8, false},
		{"not prime 9", 9, false},
		{"negative", -5, false},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			result := IsPrime(tc.input)
			if result != tc.expected {
				t.Errorf("IsPrime(%d) = %v; want %v", tc.input, result, tc.expected)
			}
		})
	}
}

// TestFactorial 表格驱动测试
func TestFactorial(t *testing.T) {
	tests := []struct {
		input    int
		expected int
	}{
		{0, 1},
		{1, 1},
		{5, 120},
		{10, 3628800},
		{-1, -1}, // 错误情况
	}

	for _, tt := range tests {
		t.Run(fmt.Sprintf("factorial_%d", tt.input), func(t *testing.T) {
			result := Factorial(tt.input)
			if result != tt.expected {
				t.Errorf("Factorial(%d) = %d; want %d", tt.input, result, tt.expected)
			}
		})
	}
}

// TestSqrt 测试浮点数
func TestSqrt(t *testing.T) {
	result, err := Sqrt(16)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != 4.0 {
		t.Errorf("Sqrt(16) = %f; want 4.0", result)
	}

	// 测试负数
	_, err = Sqrt(-1)
	if err == nil {
		t.Error("expected error for negative input")
	}
}

// BenchmarkAdd 基准测试
func BenchmarkAdd(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Add(100, 200)
	}
}

// BenchmarkIsPrime 基准测试
func BenchmarkIsPrime(b *testing.B) {
	for i := 0; i < b.N; i++ {
		IsPrime(97)
	}
}

// BenchmarkFactorial 基准测试
func BenchmarkFactorial(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Factorial(10)
	}
}

// ExampleAdd 示例函数
func ExampleAdd() {
	result := Add(2, 3)
	fmt.Println(result)
	// Output: 5
}

// ExampleDivide 示例函数
func ExampleDivide() {
	result, _ := Divide(10, 2)
	fmt.Println(result)
	// Output: 5
}

// ExampleIsPrime 示例函数
func ExampleIsPrime() {
	fmt.Println(IsPrime(7))
	fmt.Println(IsPrime(8))
	// Output:
	// true
	// false
}

// TestMain 测试主函数（可选）
// 可以在所有测试前后执行设置和清理工作
func TestMain(m *testing.M) {
	// 测试前的设置
	fmt.Println("Setting up tests...")
	
	// 运行测试
	code := m.Run()
	
	// 测试后的清理
	fmt.Println("Cleaning up after tests...")
	
	// 退出
	// os.Exit(code)
	_ = code
}

