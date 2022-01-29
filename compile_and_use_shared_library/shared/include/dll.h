#ifndef DLL_H
#define DLL_H
#define MODULE_API __declspec(dllexport)

#ifdef __cplusplus
extern "C" {
#endif

MODULE_API int add(int a, int b);

#ifdef __cplusplus
}
#endif

#endif