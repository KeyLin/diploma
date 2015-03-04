#include <stdio.h>
int main()
{
      printf( "%lu\n", (unsigned long)sizeof(int) * 8 );  /* 输出 int 的位数 */
      printf( "%zu\n", sizeof(short) * 8 );  /* 输出 short 的位数 */
      return 0;
}
