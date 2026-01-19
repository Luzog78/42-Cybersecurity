<div align="center">

# 42 Cursus - Cybersecurity: Reverse me

<img src="https://upload.wikimedia.org/wikipedia/commons/7/7f/GDB_Archer_Fish_by_Andreas_Arnez.svg" height="30" alt="GDB" />
<img width="12" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/c/c-original.svg" height="30" alt="C" />
<img width="12" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" height="30" alt="vscode" />

<br><br>

</div>


## Overview

- **Summary:** *The reverse passion. Discover the art of Reversing Engineering.*
- **Version:** *1.00*
- **Subject:** [en.subject.pdf](https://cdn.intra.42.fr/pdf/pdf/88970/en.subject.pdf)
- **Author(s):** *[ysabik](https://profile.intra.42.fr/users/ysabik)*
- **Public repo:** [GitHub](https://github.com/Luzog78/42-Cybersecurity)

<br>

- [[Reverse me]](#42-cursus---cybersecurity-reverse-me)
	- [[Installation]](#installation)
	- [[Overview]](#overview)
	- [[Level 1]](#level-1)
	- [[Level 2]](#level-2)
	- [[Level 3]](#level-3)


<br><br>

## Installation

There is no installation process for this project. <br>
You can simply clone the repository and start working on the provided files.


<br><br>

## Overview

The project consists of multiple levels, each designed to teach different aspects of reverse engineering.

In each level, a given binary is provided. When executed, it asks for a password. <br>
The goal is to analyze it, understand its behavior, find a correct password and create a source file in C that replicates the behavior of it. <br>
There can be multiple passwords but only one is necessary.


<br><br>

## Level 1

- [Password file](./level1/password)
- [Source file](./level1/source.c)

<details>
<summary>Notes (password spoiler alert!)</summary>
<pre>
/*
 * No special notes.
 *
 * Final password: "__stack_check"
 */
</pre>
</details>


<br><br>

## Level 2

- [Password file](./level2/password)
- [Source file](./level2/source.c)

<details>
<summary>Notes (password spoiler alert!)</summary>
<pre>
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
 * The goal is to have "delabere" in `str` at the end.
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
 */
</pre>
</details>


<br><br>

## Level 3

- [Password file](./level3/password)
- [Source file](./level3/source.c)

<details>
<summary>Notes (password spoiler alert!)</summary>
<pre>
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
 * The goal is to have "********" in `str` at the end.
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
 */
</pre>
</details>


<br><br>

---

<sup><i>This is an educational project proposed by 42 School through the 42Cursus program.</i><sup>
