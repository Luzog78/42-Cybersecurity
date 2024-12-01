/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   source.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/11/30 16:10:05 by ysabik            #+#    #+#             */
/*   Updated: 2024/12/01 02:49:25 by ysabik           ###   ########.fr       */
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
 * Nearly the same thing as `level2`, but in 64 bits,
 *  and with a different password.
 *
 * > "42" to pass `test_1` and `test_2`
 *
 * > "*" is already in `str`
 * > "042" to add "*"
 * > "042" to add "*"
 * > "042" to add "*"
 * > "042" to add "*"
 * > "042" to add "*"
 * > "042" to add "*"
 * > "042" to add "*"
 *
 * Final password: "42042042042042042042042"
 *
 */

// bits 64

void no() {
	puts("Nope.");
	exit(1);
}

int ok() {
	return puts("Good job.");
}

int main() {
	int		ret;
	int		i;
	int		j;
	char	str[9];
	char	buff[24];
	char	str2[4];
	char	c;
	int		k;

	size_t	_;
	int		__;

	printf("Please enter key: ");
	ret = scanf("%23s", buff);
	if (1 == ret)
		goto read_success;
	no();

read_success:
	if ('2' == buff[1])				// movsbl -0x3f(rbp), ecx; cmp ecx, 0x32
		goto test_1;
	no();

test_1:
	if ('4' == buff[0])				// movsbl -0x40(rbp), ecx; cmp ecx, 0x34
		goto test_2;
	no();

test_2:
	fflush(stdin);
	memset(str, 0, 9);
	str[0] = '*';					// movb 0x2a, -0x21(rbp)
	str2[3] = '\0';
	j = 2;
	i = 1;

go_back:
	_ = strlen(str);
	c = 0;
	if (_ >= 8)
		goto test_3;

	k = j;
	_ = strlen(buff);
	c = k < _;

test_3:
	if (c & 1)
		goto test_4;
	goto next_step;

test_4:
	str2[0] = buff[j];
	str2[1] = (buff + 1)[j];
	str2[2] = (buff + 2)[j];

	__ = atoi(str2);
	str[i] = (char) __;

	j += 3;

	i += 1;
	goto go_back;

next_step:
	str[i] = '\0';

	_ = strcmp(str, "********");	// MODIFIED
	if (_ != 0)
		goto fail;
	ok();
	goto end;

fail:
	no();

end:
	return 0;
}
