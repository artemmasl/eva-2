<template>
  <footer class="mx-auto mt-12 max-w-[1240px]">
    <div class="grid grid-cols-[auto_1.3fr_1fr_1fr] items-center gap-10 rounded-[28px] bg-white px-9 py-7 max-[900px]:grid-cols-1 max-[900px]:gap-6">
      <RouterLink class="grid h-[42px] w-[42px] place-items-center text-[34px] font-black text-[#0b2447] no-underline" to="/">A</RouterLink>

      <div class="flex flex-wrap gap-x-[18px] gap-y-2 text-xs text-[#111827] [&_a]:text-[#2348ff] [&_a]:no-underline [&_span]:w-full">
        <span>Отдел продаж:</span>
        <a href="tel:+73833121029">+7 (383) 312-10-29</a>
        <a href="mailto:help@atlas.com">help@atlas.com</a>
        <a href="https://atlas.com">www.atlas.com</a>
      </div>

      <nav class="flex flex-wrap gap-x-[18px] gap-y-2 text-xs text-[#111827] [&_a]:text-[#2348ff] [&_a]:no-underline [&_span]:w-full" aria-label="Footer objects navigation">
        <span>Объекты</span>
        <a href="#">Квартиры</a>
        <a href="#">Парковки</a>
        <a href="#">Кладовки</a>
        <a href="#">Коммерция</a>
      </nav>

      <nav class="flex flex-wrap gap-x-[18px] gap-y-2 text-xs text-[#111827] [&_a]:text-[#2348ff] [&_a]:no-underline [&_span]:w-full" aria-label="Footer tenants navigation">
        <span>Для агентов</span>
        <a href="#">Зафиксировать клиента</a>
        <a href="#">Регистрация агента</a>
      </nav>
    </div>

    <div class="flex flex-wrap justify-between gap-4 px-7 pt-6 text-[11px] text-[#6b7280] [&_a]:text-[#2348ff] [&_a]:no-underline">
      <span>©2026 Строительная компания Atlas Development</span>
      <a href="#">Использование cookie</a>
      <a href="#">Политика конфиденциальности</a>
      <span>Разработано на платформе</span>
    </div>
  </footer>
</template>
