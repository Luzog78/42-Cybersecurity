/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   source.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ysabik <ysabik@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/11/30 14:36:12 by ysabik            #+#    #+#             */
/*   Updated: 2024/11/30 16:07:03 by ysabik           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>

// bits 32
int main() {
									// sub esp, 0x84: 0x80 bytes for local vars
	char	buff[100];				// located at -0x6c(ebp): 0x6c-0x8=100
	char	*key = "__stack_check";	// located at -0x7a(ebp)

	printf("Please enter key: ");	// call <printf@plt>
	scanf("%s", buff);				// call <_iso99_scanf@plt>

	int ret = strcmp(buff, key);	// call <strcmp@plt>
	if (ret != 0)					// cmp 0, eax
		goto fail;					// jmp <main+160>

	printf("Good job.\n");			// call <printf@plt>
	goto end;						// jmp <main+177>

fail:								// <main+160>
	printf("Nope.\n");				// call <printf@plt>

end:								// <main+177>
	return 0;						// xor eax, eax
}
