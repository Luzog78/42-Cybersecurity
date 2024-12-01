/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   source.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/11/30 16:10:05 by ysabik            #+#    #+#             */
/*   Updated: 2024/12/01 02:15:49 by ysabik           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * **************************************
 * ******** PASSWORD EXPLANATION ********
 * **************************************
 *
 * > "00" to pass `test_1` and `test_2`
 *
 * Next, password is read 3 by 3 until the end of the buffer.
 * Interprets the 3 characters as char-integers.
 * Then adds the found char to `str`.
 *
 * > "d" is already in `str`
 * > "101" to add "e"
 * > "108" to add "l"
 * > "097" to add "a"
 * > "098" to add "b"
 * > "101" to add "e"
 * > "114" to add "r"
 * > "101" to add "e"
 *
 * Final password: "00101108097098101114101"
 *
 */

// bits 32

void no() {
						// sub esp, 0x14: 0x10 bytes for local vars
	puts("Nope.");		// call <puts@plt>
	exit(1);			// movl 0x1, esp; call <exit@plt>
}

int xd() {
						// sub esp, 0x14: 0x10 bytes for local vars
	puts("...");		// call <puts@plt>
	return puts("...");	// call <puts@plt>
}

int ok() {
	return puts("Good job.");	// call <puts@plt>
}

int main() {
									// sub esp, 0x54: 0x50 bytes for local vars
	int		ret;					// located at -0xc(ebp)
	int		i;						// located at -0x10(ebp)
	int		j;						// located at -0x14(ebp)
	char	str[9];					// located at -0x1d(ebp), sized by memset
	char	buff[24];				// located at -0x35(ebp), size deduced
	char	str2[4];				// located at -0x39(ebp), sized by atoi
									// ... memory gap (1 byte) ...
	char	c;						// located at -0x41(ebp)
									// ... memory gap (3 bytes) ...
	int		k;						// located at -0x48(ebp)

	size_t	_;						// temp var == register
	int		__;						// temp var == register

	printf("Please enter key: ");	// call <printf@plt>
	ret = scanf("%23s", buff);		// call <__isoc99_scanf@plt>
	if (1 == ret)					// cmp -0xc(ebp), 0x1
		goto read_success;			// je <main+92>
	no();							// call <no>

read_success:						// <main+92>
	if ('0' == buff[1])				// movsbl -0x34(ebp), ecx; cmp ecx, 0x30
		goto test_1;				// je <main+117>
	no();

test_1:								// <main+117>
	if ('0' == buff[0])				// movsbl -0x35(ebp), ecx; cmp ecx, 0x30
		goto test_2;				// je <main+142>
	no();

test_2:								// <main+142>
	fflush(stdin);					// call <fflush@plt> (_IO_2_1_stdin_)
									// mov -0x1d(ebp), (esp) -> args[0] = str
									// mov 0x0, 0x4(esp) -> args[1] = 0
									// mov 0x9, 0x8(esp) -> args[2] = 9
	memset(str, 0, 9);				// call <memset@plt>
	str[0] = 'd';					// movb 0x64, -0x1d(ebp)
	str2[3] = '\0';					// movb 0x0, -0x36(ebp)
	j = 2;							// movl 0x2, -0x14(ebp)
	i = 1;							// movl 0x1, -0x10(ebp)

go_back:							// <main+221>
									// mov -0x1d(ebp), (esp) -> args[0] = str
	_ = strlen(str);				// call <strlen@plt>
									// mov eax, ecx; xor eax, eax
	c = 0;							// mov al, -0x41(ebp)
	if (_ >= 8)						// cmp 0x8, ecx
		goto test_3;				// jae <main+286>

	k = j;							// mov -0x14(ebp), eax; mov eax, -0x48(ebp)
									// mov -0x35(ebp), (esp) -> args[0] = buff
	_ = strlen(buff);				// call <strlen@plt>
									// cmp eax, -0x48(ebp)
	c = k < _;						// setb al; mov al, -0x41(ebp)

test_3:								// <main+286>
	if (c & 1)						// test 0x1, al  (==> comp 0x0, (al & 0x1))
		goto test_4;				// jne <main+302>
	goto next_step;					// jmp <main+378>

test_4:								// <main+302>
	str2[0] = buff[j];				// mov -0x35(ebp, -0x14(ebp), 1), -0x39(ebp)
	str2[1] = (buff + 1)[j];		// mov -0x34(ebp, -0x14(ebp), 1), -0x38(ebp)
	str2[2] = (buff + 2)[j];		// mov -0x33(ebp, -0x14(ebp), 1), -0x37(ebp)
									// mov -0x39(ebp), (esp) -> args[0] = str2
	__ = atoi(str2);				// call <atoi@plt>
	str[i] = (char) __;				// mov al, -0x1d(ebp, -0x10(ebp), 1)
									// mov -0x14(ebp), eax; add 0x3, eax
	j += 3;							// mov eax, -0x14(ebp)
									// mov -0x10(ebp), eax; add 0x1, eax
	i += 1;							// mov eax, -0x10(ebp)
	goto go_back;					// jmp <main+221>

next_step:							// <main+378>
	str[i] = '\0';					// movb 0x0, -0x1d(ebp, -0x10(ebp), 1)
									// mov -0x1d(ebp), (esp) -> args[0] = str
	_ = strcmp(str, "delabere");	// call <strcmp@plt>
	if (_ != 0)						// cmp 0x0, eax
		goto fail;					// jne <main+432>
	ok();							// call <ok>
	goto end;						// jmp <main+440>

fail:								// <main+432>
	no();							// call <no>

end:								// <main+440>
	return 0;						// xor eax, eax
}

int xxd() {
						// sub esp, 0x14: 0x10 bytes for local vars
	puts("...");		// call <puts@plt>
	return puts("...");	// call <puts@plt>
}

int n() {
	return puts("...");	// call <puts@plt>
}

int xxxd() {
						// sub esp, 0x14: 0x10 bytes for local vars
	puts("...");		// call <puts@plt>
	return puts("...");	// call <puts@plt>
}

int ww() {
						// sub esp, 0x14: 0x10 bytes for local vars
	puts("...");		// call <puts@plt>
	puts("...");		// call <puts@plt>
	puts("...");		// call <puts@plt>
	puts("...");		// call <puts@plt>
	return puts("...");	// call <puts@plt>
}

int xyxxd() {
						// sub esp, 0x14: 0x10 bytes for local vars
	puts("...");		// call <puts@plt>
	return puts("...");	// call <puts@plt>
}
