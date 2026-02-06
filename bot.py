Traceback (most recent call last):
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/site-packages/telegram/ext/_application.py", line 921, in __run
    raise exc
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/site-packages/telegram/ext/_application.py", line 910, in __run
    loop.run_until_complete(self.initialize())
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/asyncio/base_events.py", line 701, in run_until_complete
    self._check_running()
    ~~~~~~~~~~~~~~~~~~~^^
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/asyncio/base_events.py", line 637, in _check_running
    raise RuntimeError('This event loop is already running')RuntimeError: This event loop is already running

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/site-packages/telegram/ext/_application.py", line 932, in __run
    loop.run_until_complete(self.shutdown())
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/asyncio/base_events.py", line 701, in run_until_complete
    self._check_running()
    ~~~~~~~~~~~~~~~~~~~^^
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/asyncio/base_events.py", line 637, in _check_running
    raise RuntimeError('This event loop is already running')RuntimeError: This event loop is already running

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/data/user/0/ru.iiec.pydroid3/files/accomp_files/iiec_run/iiec_run.py", line 31, in <module>
    start(fakepyfile,mainpyfile)
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/data/user/0/ru.iiec.pydroid3/files/accomp_files/iiec_run/iiec_run.py", line 30, in start
    exec(open(mainpyfile).read(),  __main__.__dict__)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 125, in <module>
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/asyncio/base_events.py", line 725, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "<string>", line 122, in main
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/site-packages/telegram/ext/_application.py", line 727, in run_polling
    return self.__run(
           ~~~~~~~~~~^
        updater_coroutine=self.updater.start_polling(
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<12 lines>...
        stop_signals=stop_signals,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/site-packages/telegram/ext/_application.py", line 937, in __run
    loop.close()
    ~~~~~~~~~~^^
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/asyncio/unix_events.py", line 70, in close
    super().close()
    ~~~~~~~~~~~~~^^
  File "/data/user/0/ru.iiec.pydroid3/files/aarch64-linux-android/lib/python3.13/asyncio/selector_events.py", line 101, in close
    raise RuntimeError("Cannot close a running event loop")
RuntimeError: Cannot close a running event loop
<sys>:0: RuntimeWarning: coroutine 'Application.shutdown' was never awaited
<sys>:0: RuntimeWarning: coroutine 'Application.initialize' was never awaited

[Program finished]
